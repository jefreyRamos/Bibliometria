"""Prueba de las cuatro secciones y casos límite con Streamlit AppTest."""
from pathlib import Path
from streamlit.testing.v1 import AppTest


def comprobar(app):
    assert not app.exception, [e.message for e in app.exception]
    assert not app.error, [e.value for e in app.error]


app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=60).run()
comprobar(app)
app.selectbox[0].select(6).run(); comprobar(app)
app.selectbox[0].select(8).run(); comprobar(app)
app.radio[0].set_value('R1 · Similitud').run(); comprobar(app)
app.multiselect[0].set_value([0,6,8]).run(); comprobar(app)
assert len(app.dataframe[0].value) == 3
app.multiselect[0].set_value([0]).run(); comprobar(app)
assert app.warning
app.radio[0].set_value('R2 · Clustering').run(); comprobar(app)
for enlace in ['single','complete','average']:
    app.radio[1].set_value(enlace).run(); comprobar(app)
    assert len(app.dataframe[0].value) == 3
app.slider[0].set_value(6).run(); comprobar(app)
app.radio[0].set_value('R3 · Búsqueda de patrones').run(); comprobar(app)
for patron in ['', 'generative', 'x'*2000, 'Artificial']:
    app.text_input[0].set_value(patron).run(); comprobar(app)
    if patron:
        resumen=app.dataframe[0].value
        assert len(set(resumen['Apariciones'])) == 1
app.checkbox[0].check().run(); comprobar(app)
print('AppTest: cuatro secciones, selección múltiple, tres enlaces, k=6, patrón vacío, largo, sensible a mayúsculas y opción minúsculas: OK')

