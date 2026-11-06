//! Vault boundary only. Never store unencrypted secrets in this scaffold.
use nolp_contracts::{Module, ModuleState};

pub struct VaultUnavailable;
impl Module for VaultUnavailable {
    fn id(&self) -> &'static str {
        "vault"
    }
    fn state(&self) -> ModuleState {
        ModuleState::Unavailable
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn not_claimed_ready() {
        assert_eq!(VaultUnavailable.state(), ModuleState::Unavailable);
    }
}
