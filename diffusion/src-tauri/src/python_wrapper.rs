use pyo3::prelude::*;
use pyo3::PyResult;

pub fn py_get_python_dir() -> PyResult<String> {
    Python::with_gil(|py| {
        let sys = py.import("sys")?;
        let executable = sys.getattr("executable")?.extract()?;

        Ok(executable)
    })
}