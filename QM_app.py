import csv
import io
import os
import hashlib
import hmac
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from core import connect, import_staff, submit, export_pdfs, load_requirements, read_staff

st.set_page_config(page_title='Belehrungen · KGE, CMTD & GYN', page_icon='📋', layout='wide')
st.title('Belehrungen · KGE, CMTD & GYN')
st.caption('Jährliche Nachweise zentral einreichen und ihren Status verfolgen.')
with connect(os.environ.get('BELEHRUNGEN_DB', 'data/belehrungen_ohne_login.db')) as db:
    db.execute('CREATE TABLE IF NOT EXISTS app_settings(key TEXT PRIMARY KEY, value TEXT NOT NULL)')
    roster_path = Path(__file__).resolve().parent / 'mitarbeiter.csv'
    if not roster_path.exists():
        st.error('mitarbeiter.csv fehlt. Bitte die CSV im selben Ordner wie QM_app.py ablegen.')
        st.stop()
    try:
        roster_bytes = roster_path.read_bytes()
        roster_hash = hashlib.sha256(roster_bytes).hexdigest()
        previous = db.execute("SELECT value FROM app_settings WHERE key='roster_hash'").fetchone()
        if previous is None or previous['value'] != roster_hash:
            import_staff(db, roster_bytes, 'csv-datei')
            with db:
                db.execute("INSERT INTO app_settings VALUES('roster_hash',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (roster_hash,))
        roster_ids = [r['subject'] for r in read_staff(roster_bytes)]
    except (OSError, ValueError, UnicodeError, csv.Error) as exc:
        st.error(f'mitarbeiter.csv konnte nicht geladen werden: {exc}')
        st.stop()
    view = st.sidebar.radio('Ansicht wählen', ['Mitarbeiter', 'Verwaltung'])
    admin = False

    if view == 'Verwaltung':
        # Dummy password for testing only. Visible to repository readers.
        expected_password = "Test123!"

        def check_password():
            entered = st.session_state.pop("verwaltung_password", "")
            st.session_state["verwaltung_authenticated"] = hmac.compare_digest(
                entered.encode("utf-8"), expected_password.encode("utf-8")
            )

        def logout():
            st.session_state.pop("verwaltung_authenticated", None)
            st.session_state.pop("verwaltung_password", None)

        if not st.session_state.get("verwaltung_authenticated", False):
            st.sidebar.text_input(
                "Verwaltungspasswort", type="password",
                key="verwaltung_password", on_change=check_password,
            )
            if not st.session_state.get("verwaltung_authenticated", False):
                if st.session_state.get("verwaltung_authenticated") is False:
                    st.sidebar.error("Passwort falsch.")
                st.info("Passwort eingeben und Enter drücken.")
                st.stop()

        admin = True
        st.sidebar.button("Verwaltung abmelden", on_click=logout)
    employee = None
    subject = 'verwaltung-testlogin'
    if not admin:
        staff_choices = [r for r in db.execute('SELECT * FROM employees ORDER BY nachname,vorname,subject') if r['subject'] in roster_ids]
        if not staff_choices:
            st.info('Bitte Mitarbeiter in mitarbeiter.csv neben QM_app.py eintragen.')
            st.stop()
        selected = st.sidebar.selectbox('Mitarbeiter auswählen', range(len(staff_choices)), format_func=lambda i: f"{staff_choices[i]['vorname']} {staff_choices[i]['nachname']} · {staff_choices[i]['bereich']} · {staff_choices[i]['subject']}")
        employee = staff_choices[selected]
        subject = employee['subject']
    try:
        yearly_topics = load_requirements(Path(__file__).resolve().parent / 'pflichtbelehrungen.csv')
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        st.error(f'pflichtbelehrungen.csv konnte nicht geladen werden: {exc}')
        st.stop()
    years = sorted(yearly_topics, reverse=True)
    current_year = datetime.now(ZoneInfo('Europe/Berlin')).year
    default_index = years.index(current_year) if current_year in years else 0
    year = st.sidebar.selectbox('Belehrungsjahr', years, index=default_index)
    topics = yearly_topics[year]
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
        st.caption('Uploads zählen als eingereicht. Bei Status Rückfrage kann eine korrigierte PDF erneut hochgeladen werden. Die Verwaltung prüft und bestätigt den Nachweis.')
        if st.button('Nachweise verbindlich einreichen', disabled=not files or not topics):
            for file in files:
                try:
                    submit(db, subject, file.name, file.getvalue(), year, topics)
                    st.success(f'{file.name}: eingereicht')
                except ValueError as exc:
                    st.error(f'{file.name}: {exc}')
    elif page == 'Gesamtübersicht' and admin:
        st.subheader(f'Gesamtübersicht {year}')
        department = st.selectbox('Bereich filtern', ['Alle', 'KGE', 'CMTD', 'GYN'])
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
        st.subheader('PDFs als Ordner herunterladen')
        scope = st.radio('ZIP-Inhalt', ['Alle PDFs aus allen Jahren und Bereichen', 'Gewähltes Jahr und gefilterter Bereich'])
        if st.button('ZIP erstellen'):
            all_records = scope == 'Alle PDFs aus allen Jahren und Bereichen'
            archive, count = export_pdfs(db, year=None if all_records else year,
                                         department=None if all_records or department == 'Alle' else department)
            if count:
                st.success(f'{count} PDFs bereit. Nach dem Download die ZIP-Datei entpacken.')
                st.download_button('ZIP herunterladen', archive,
                                   'Belehrungen_Alle.zip' if all_records else f'Belehrungen_{year}_{department}.zip',
                                   'application/zip')
            else:
                st.info('Für diese Auswahl sind keine PDFs vorhanden.')
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
        st.subheader('Pflichtbelehrungen aus CSV')
        st.caption('Die Jahreskonfiguration wird ausschließlich in pflichtbelehrungen.csv neben QM_app.py gepflegt. Änderungen werden beim nächsten Laden übernommen.')
        st.dataframe([{'Jahr': year, 'Belehrung': topic} for topic in topics], hide_index=True)
        st.subheader('Mitarbeiterliste')
        st.write('Die Mitarbeiter werden automatisch aus mitarbeiter.csv im selben Ordner wie QM_app.py geladen. Änderungen an der Datei werden beim nächsten Laden übernommen. Die Mitarbeiter-ID (CSV-Spalte Mitarbeiter-ID) muss pro Person eindeutig und dauerhaft gleich bleiben.')
        employee_rows = [
            {
                'Mitarbeiter-ID': r['subject'],
                'Nachname': r['nachname'],
                'Vorname': r['vorname'],
                'Bereich': r['bereich'],
            }
            for r in db.execute('SELECT * FROM employees ORDER BY nachname,vorname')
            if r['subject'] in roster_ids
        ]
        st.dataframe(employee_rows, hide_index=True)
        st.caption('Aus der CSV entfernte Personen sind nicht mehr auswählbar. Bereits gespeicherte Nachweise bleiben für den Export und die Gesamtübersicht erhalten.')