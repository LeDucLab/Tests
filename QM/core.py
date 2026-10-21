import csv
import io
import re
import sqlite3
import unicodedata
from pathlib import Path

TOPICS = ['Datenschutz', 'Compliance', 'Händehygiene', 'Brandschutz', 'Arbeitsschutz', 'Energiemanagement']

def norm(value):
    value = value.casefold().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    return ''.join(c for c in unicodedata.normalize('NFKD', value) if c.isalnum())

def recognize(filename, employee):
    parts = Path(filename).stem.split('_')
    if len(parts) != 4 or not re.fullmatch(r'20\d{2}', parts[-1]):
        raise ValueError('Erwartet: Belehrung_Nachname_Vorname_Jahr.pdf (Belehrung durch die konkrete Art ersetzen).')
    topic = next((t for t in TOPICS if norm(t) == norm(parts[0])), None)
    if not topic:
        raise ValueError('Belehrungsart nicht erkannt.')
    if norm(parts[1]) != norm(employee['nachname']) or norm(parts[2]) != norm(employee['vorname']):
        raise ValueError('Der Name im Dateinamen gehört nicht zum angemeldeten Mitarbeiter.')
    return topic, int(parts[-1])

def connect(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=20)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript('''
    CREATE TABLE IF NOT EXISTS employees(subject TEXT PRIMARY KEY, nachname TEXT NOT NULL, vorname TEXT NOT NULL, bereich TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS requirements(year INTEGER PRIMARY KEY, topics TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS evidence(id INTEGER PRIMARY KEY, subject TEXT NOT NULL REFERENCES employees(subject), topic TEXT NOT NULL, year INTEGER NOT NULL, filename TEXT NOT NULL, body BLOB NOT NULL, status TEXT NOT NULL DEFAULT 'Eingereicht', submitted TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, reviewer TEXT, reviewed TEXT, UNIQUE(subject,topic,year));
    CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY, actor TEXT NOT NULL, action TEXT NOT NULL, at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
    ''')
    return db

def import_staff(db, content, actor):
    rows = list(csv.DictReader(io.StringIO(content.decode('utf-8-sig')), delimiter=';'))
    required = {'subject', 'nachname', 'vorname', 'bereich'}
    if not rows or not required.issubset(rows[0]):
        raise ValueError('Spalten benötigt: subject;nachname;vorname;bereich')
    seen = set()
    for row in rows:
        if any(not (row.get(k) or '').strip() for k in required) or row['bereich'].strip() not in ['CMTD', 'GYN']:
            raise ValueError('Alle Felder ausfüllen; Bereich muss CMTD oder GYN sein.')
        if row['subject'].strip() in seen:
            raise ValueError('Doppelte subject-ID in der Mitarbeiterliste.')
        seen.add(row['subject'].strip())
    with db:
        for r in rows:
            db.execute('INSERT INTO employees VALUES(?,?,?,?) ON CONFLICT(subject) DO UPDATE SET nachname=excluded.nachname,vorname=excluded.vorname,bereich=excluded.bereich', tuple(r[k].strip() for k in ['subject','nachname','vorname','bereich']))
        db.execute('INSERT INTO audit(actor,action) VALUES(?,?)', (actor, f'Mitarbeiterimport: {len(rows)}'))
    return len(rows)

def submit(db, actor, filename, data, year, topics):
    employee = db.execute('SELECT * FROM employees WHERE subject=?', (actor,)).fetchone()
    if employee is None:
        raise ValueError('Kein Mitarbeiterkonto freigeschaltet.')
    topic, file_year = recognize(filename, employee)
    if file_year != year or topic not in topics:
        raise ValueError('Jahr oder Belehrung entspricht nicht den gewählten Pflichtbelehrungen.')
    if Path(filename).suffix.lower() != '.pdf' or not data.startswith(b'%PDF-') or len(data) > 10 * 1024 * 1024:
        raise ValueError('Bitte eine PDF-Datei mit höchstens 10 MB hochladen.')
    with db:
        try:
            db.execute('INSERT INTO evidence(subject,topic,year,filename,body) VALUES(?,?,?,?,?)', (actor, topic, year, Path(filename).name, data))
        except sqlite3.IntegrityError as exc:
            raise ValueError('Für diese Belehrung und dieses Jahr liegt bereits ein Nachweis vor. Bitte Verwaltung kontaktieren.') from exc
        db.execute('INSERT INTO audit(actor,action) VALUES(?,?)', (actor, f'Eingereicht: {topic}, {year}'))


def export_pdfs(db, year=None, department=None):
    """Create a ZIP with safe, unique paths and the original PDF bytes."""
    import zipfile
    def safe(value):
        return re.sub(r'[^\w .-]', '_', str(value)).strip(' .')[:100] or 'Unbekannt'
    query = '''SELECT e.id,e.year,e.topic,e.body,m.nachname,m.vorname,m.bereich
               FROM evidence e JOIN employees m ON m.subject=e.subject WHERE 1=1'''
    args = []
    if year is not None:
        query += ' AND e.year=?'
        args.append(year)
    if department is not None:
        query += ' AND m.bereich=?'
        args.append(department)
    query += ' ORDER BY e.year,m.bereich,m.nachname,m.vorname,e.id'
    output = io.BytesIO()
    count = 0
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        for row in db.execute(query, args):
            # The evidence ID avoids collisions even for identical employee names.
            name = f"{row['year']}/{safe(row['bereich'])}/{safe(row['nachname'])}_{safe(row['vorname'])}/{safe(row['topic'])}_{row['id']}.pdf"
            archive.writestr(name, row['body'])
            count += 1
    return output.getvalue(), count
