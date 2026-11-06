//! Local profile identity metadata only. Persistence is not implemented.
use nolp_contracts::{Module, ModuleState};

pub struct LocalProfile {
    pub label: String,
}
impl LocalProfile {
    pub fn new(label: impl Into<String>) -> Self {
        Self {
            label: label.into(),
        }
    }
}
impl Module for LocalProfile {
    fn id(&self) -> &'static str {
        "identity-local"
    }
    fn state(&self) -> ModuleState {
        ModuleState::Unavailable
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn label() {
        assert_eq!(LocalProfile::new("local").label, "local");
    }
}
