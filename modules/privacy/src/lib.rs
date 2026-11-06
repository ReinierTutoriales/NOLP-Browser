//! Conservative local policy for optional remote account services.
use nolp_contracts::{Module, ModuleState};

#[derive(Default)]
pub struct Privacy {
    pub sync_opt_in: bool,
}
impl Module for Privacy {
    fn id(&self) -> &'static str {
        "privacy"
    }
    fn state(&self) -> ModuleState {
        ModuleState::Unavailable
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn sync_disabled() {
        assert!(!Privacy::default().sync_opt_in);
    }
}
