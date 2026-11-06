//! Portable NOLP boundaries. No Gecko, UI or network dependencies.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Decision {
    Allow,
    Block,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Capability {
    Navigate,
    Filter,
    PrivateProfile,
    LocalVault,
    Playback,
    Update,
}
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Request<'a> {
    pub host: &'a str,
    pub private: bool,
}
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Verdict {
    pub decision: Decision,
    pub reason: &'static str,
}
pub trait Policy: Send + Sync {
    fn evaluate(&self, request: &Request<'_>) -> Verdict;
}
pub trait Engine: Send + Sync {
    fn available(&self) -> bool;
}
pub trait Surface: Send + Sync {
    fn theme(&self) -> Theme;
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Theme {
    AeroLight,
    AeroDark,
}
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ModuleState {
    Scaffold,
    Ready,
    Unavailable,
    RequiresConsent,
}
impl ModuleState {
    pub const fn is_operational(self) -> bool {
        matches!(self, Self::Ready)
    }
}
pub trait Module: Send + Sync {
    fn id(&self) -> &'static str;
    fn state(&self) -> ModuleState;
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn contract_values() {
        assert_ne!(Decision::Allow, Decision::Block);
        assert_ne!(Theme::AeroLight, Theme::AeroDark);
        assert!(!ModuleState::Scaffold.is_operational());
        assert!(!ModuleState::Unavailable.is_operational());
        assert!(!ModuleState::RequiresConsent.is_operational());
        assert!(ModuleState::Ready.is_operational());
    }
}
