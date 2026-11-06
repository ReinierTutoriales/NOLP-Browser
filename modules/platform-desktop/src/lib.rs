//! Desktop platform adapter placeholder; Firefox chrome UI not connected.
use nolp_contracts::{Module, ModuleState};

pub struct DesktopUnavailable;
impl Module for DesktopUnavailable {
    fn id(&self) -> &'static str {
        "platform-desktop"
    }
    fn state(&self) -> ModuleState {
        ModuleState::Scaffold
    }
}
