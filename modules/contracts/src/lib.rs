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
/// Conservative ASCII DNS validation for the offline policy prototype.
/// Internationalized hostnames must be converted to IDNA ASCII by the caller.
pub fn normalized_dns_host(host: &str) -> Option<String> {
    let host = host.trim().trim_end_matches('.');
    if host.is_empty()
        || host.len() > 253
        || !host.is_ascii()
        || host.parse::<std::net::IpAddr>().is_ok()
    {
        return None;
    }
    for label in host.split('.') {
        if label.is_empty()
            || label.len() > 63
            || label.starts_with('-')
            || label.ends_with('-')
            || !label
                .bytes()
                .all(|b| b.is_ascii_alphanumeric() || b == b'-')
        {
            return None;
        }
    }
    Some(host.to_ascii_lowercase())
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
    fn invalid_dns_hosts_rejected() {
        for host in [
            "",
            "https://example.com",
            "example.com/path",
            "a..b",
            "-bad.example",
            "127.0.0.1",
            "bücher.example",
        ] {
            assert_eq!(normalized_dns_host(host), None);
        }
        assert_eq!(
            normalized_dns_host("EXAMPLE.COM."),
            Some("example.com".to_string())
        );
    }
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
