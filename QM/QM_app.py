import csv
import io
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from core import TOPICS, connect, import_staff, submit

st.set_page_config(page_title='Belehrungen · CMTD & GYN', page_icon='📋', layout='wide')
st.title('Belehrungen · CMTD & GYN')
st.caption('Jährliche Nachweise zentral einreichen und ihren Status verfolgen.')
st.warning('Testversion ohne Anmeldung: Alle Besucher können sämtliche Ansichten und Nachweise aufrufen und ändern. Bitte nur Testdaten verwenden.')
with connect(os.environ.get('BELEHRUNGEN_DB', 'data/belehrungen_ohne_login.db')) as db:
    db.execute('CREATE TABLE IF NOT EXISTS app_settings(key TEXT PRIMARY KEY, value TEXT NOT NULL)')
    if not db.execute("SELECT 1 FROM app_settings WHERE key='initialized'").fetchone():
        with db:
            db.executemany('INSERT OR IGNORE INTO employees VALUES(?,?,?,?)', [
                ('test-cmtd', 'Mustermann', 'Erika', 'CMTD'),
                ('test-gyn', 'Musterfrau', 'Anna', 'GYN')])
            db.execute('INSERT OR IGNORE INTO requirements VALUES(?,?)', (datetime.now(ZoneInfo('Europe/Berlin')).year, '|'.join(TOPICS)))
            db.execute("INSERT INTO app_settings VALUES('initialized','1')")
    view = st.sidebar.radio('Ansicht wählen', ['Mitarbeiter', 'Verwaltung'])
    admin = view == 'Verwaltung'
    employee = None
    subject = 'verwaltung-ohne-login'
    if not admin:
        staff_choices = db.execute('SELECT * FROM employees ORDER BY nachname,vorname,subject').fetchall()
        if not staff_choices:
            st.info('Bitte zuerst in der Verwaltung Mitarbeiter importieren.')
            st.stop()
        selected = st.sidebar.selectbox('Mitarbeiter auswählen', range(len(staff_choices)), format_func=lambda i: f"{staff_choices[i]['vorname']} {staff_choices[i]['nachname']} · {staff_choices[i]['bereich']} · {staff_choices[i]['subject']}")
        employee = staff_choices[selected]
        subject = employee['subject']
    year = st.sidebar.number_input('Belehrungsjahr', 2020, 2100, datetime.now(ZoneInfo('Europe/Berlin')).year)
    req = db.execute('SELECT topics FROM requirements WHERE year=?', (year,)).fetchone()
    topics = req['topics'].split('|') if req and req['topics'] else []
    pages = (['Meine Nachweise', 'Nachweis einreichen'] if employee else []) + (['Gesamtübersicht', 'Verwaltung'] if admin else [])
    page = st.sidebar.radio('Bereich', pages)
    if not topics:
        st.info('Für dieses Jahr wurden noch keine Pflichtbelehrungen festgelegt.')
    if page == 'Meine Nachweise':
        st.subheader(f"{employee['vorname']} {employee['nachname']} · {year}")
        own = {r['topic']: r for r in db.execute('SELECT id,topic,status,submitted FROM evidence WHERE subject=? AND year=?', (subject, year))}
        st.dataframe([{'Belehrung': t, 'Status': own[t]['status'] if t in own else 'Offen', 'Eingereicht am': own[t]['submitted'] if t in own else '—'} for t in topics], hide_index=True, use_container_width=True)
    elif page == 'Nachweis einreichen':
        st.subheader('Nachweise hochladen')
        st.write('Dateiname: Datenschutz_Nachname_Vorname_Jahr.pdf. Möglich sind die für das Jahr festgelegten Belehrungen. Keine automatische Inhaltsprüfung oder OCR.')
        files = st.file_uploader('PDF-Nachweise · maximal 10 MB je Datei', type=['pdf'], accept_multiple_files=True)
        st.caption('Uploads zählen als eingereicht. Die Verwaltung prüft und bestätigt den Nachweis.')
        if st.button('Nachweise verbindlich einreichen', disabled=not files or not topics):
            for file in files:
                try:
                    submit(db, subject, file.name, file.getvalue(), year, topics)
                    st.success(f'{file.name}: eingereicht')
                except ValueError as exc:
                    st.error(f'{file.name}: {exc}')
    elif page == 'Gesamtübersicht' and admin:
        st.subheader(f'Gesamtübersicht {year}')
        department = st.selectbox('Bereich filtern', ['Alle', 'CMTD', 'GYN'])
        staff = db.execute('SELECT * FROM employees ORDER BY nachname,vorname').fetchall()
        evidence = {(r['subject'], r['topic']): r for r in db.execute('SELECT id,subject,topic,status,filename,submitted FROM evidence WHERE year=?', (year,))}
        rows = []
        for e in staff:
            if department != 'Alle' and e['bereich'] != department:
                continue
            rows.append({'Nachname': e['nachname'], 'Vorname': e['vorname'], 'Bereich': e['bereich'], **{t: evidence[(e['subject'], t)]['status'] if (e['subject'], t) in evidence else 'Offen' for t in topics}})
        st.dataframe(rows, hide_index=True, use_container_width=True)
        if rows:
            out = io.StringIO()
            writer = csv.DictWriter(out, fieldnames=list(rows[0]), delimiter=';')
            writer.writeheader()
            for row in rows:
                writer.writerow({k: "'"+v if isinstance(v,str) and v.startswith(('=', '+', '-', '@', '\t', '\r')) else v for k,v in row.items()})
            st.download_button('Übersicht als CSV', out.getvalue().encode('utf-8-sig'), f'Belehrungen_{year}.csv', 'text/csv')
        st.subheader('Eingereichte Nachweise prüfen')
        visible = {e['subject'] for e in staff if department == 'Alle' or e['bereich'] == department}
        for r in evidence.values():
            if r['subject'] not in visible:
                continue
            with st.expander(f"{r['filename']} · {r['status']}"):
                body = db.execute('SELECT body FROM evidence WHERE id=?', (r['id'],)).fetchone()['body']
                st.download_button('PDF herunterladen', body, r['filename'], 'application/pdf', key=f"download{r['id']}")
                status = st.selectbox('Prüfergebnis', ['Eingereicht', 'Bestätigt', 'Rückfrage'], index=['Eingereicht','Bestätigt','Rückfrage'].index(r['status']), key=f"status{r['id']}")
                if st.button('Prüfergebnis speichern', key=f"save{r['id']}"):
                    with db:
                        db.execute('UPDATE evidence SET status=?,reviewer=?,reviewed=CURRENT_TIMESTAMP WHERE id=?', (status,subject,r['id']))
                        db.execute('INSERT INTO audit(actor,action) VALUES(?,?)', (subject, f"Nachweis {r['id']}: {status}"))
                    st.rerun()
    elif page == 'Verwaltung' and admin:
        st.subheader('Pflichtbelehrungen festlegen')
        chosen = st.multiselect('Pflichtbelehrungen für das gewählte Jahr', TOPICS, default=topics)
        if st.button('Jahreskonfiguration speichern'):
            with db:
                db.execute('INSERT INTO requirements VALUES(?,?) ON CONFLICT(year) DO UPDATE SET topics=excluded.topics', (year, '|'.join(chosen)))
                db.execute('INSERT INTO audit(actor,action) VALUES(?,?)', (subject, f'Pflichtbelehrungen {year}: {chosen}'))
            st.rerun()
        st.subheader('Mitarbeiterliste importieren')
        st.write('CSV mit Semikolon: subject;nachname;vorname;bereich. Bereich: CMTD oder GYN. subject ist eine frei vergebene, eindeutige Mitarbeiter-ID (z. B. MA001). Bestehende Personen werden aktualisiert; fehlende nicht gelöscht.')
        file = st.file_uploader('Mitarbeiterliste', type=['csv'])
        if st.button('Liste importieren', disabled=file is None):
            try:
                count = import_staff(db, file.getvalue(), subject)
                st.success(f'{count} Mitarbeiter übernommen.')
            except (ValueError, UnicodeError, csv.Error) as exc:
                st.error(str(exc))
