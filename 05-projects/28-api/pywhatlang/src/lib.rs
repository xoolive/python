use pyo3::{exceptions::PyRuntimeError, prelude::*};
use serde::ser::Serialize;
use serde::ser::SerializeStruct;

struct SerializedInfo(whatlang::Info);

impl Serialize for SerializedInfo {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        let mut info = serializer.serialize_struct("info", 3)?;
        info.serialize_field("lang", &self.0.lang())?;
        info.serialize_field("script", &self.0.script())?;
        info.serialize_field("confidence", &self.0.confidence())?;
        info.end()
    }
}

#[pyfunction]
fn detect(input: &str) -> PyResult<String> {
    match whatlang::detect(input) {
        Some(res) => {
            let serialized_info = SerializedInfo(res);
            Ok(serde_json::to_string(&serialized_info).unwrap())
        }
        None => Err(PyErr::new::<PyRuntimeError, _>("Language not detected")),
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn pywhatlang(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(detect, m)?)?;
    Ok(())
}
