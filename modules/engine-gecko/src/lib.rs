//! Gecko adapter boundary. Integration not yet available.
use nolp_contracts::{Engine, Module, ModuleState};

pub struct GeckoAdapter {
    integrated: bool,
}
impl GeckoAdapter {
    pub fn not_integrated() -> Self {
        Self { integrated: false }
    }
}
impl Engine for GeckoAdapter {
    fn available(&self) -> bool {
        self.integrated
    }
}
impl Module for GeckoAdapter {
    fn id(&self) -> &'static str {
        "engine-gecko"
    }
    fn state(&self) -> ModuleState {
        ModuleState::Scaffold
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn no_false_gecko_claim() {
        assert!(!GeckoAdapter::not_integrated().available());
    }
}
