import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { Button, DropdownMenu, Flex, Text } from "@radix-ui/themes";
import { PersonIcon, ExitIcon } from "@radix-ui/react-icons";
import { useAuth } from "../../context/AuthContext";
import authService from "../../services/authService";
import "./Header.css";

const Header: React.FC = () => {
  const navigate = useNavigate();
  const auth = useAuth();

  let user = null;
  let logout = async () => { };

  if (auth) {
    user = auth.user;
    logout = auth.logout;
  } else {
    console.warn("Auth context not available in Header, using fallback");
    // Fallback logout function
    logout = async () => {
      await authService.logout();
    };
  }

  const handleLogout = async () => {
    await logout();
    navigate("/login", { replace: true });
  };

  return (
    <header className="app-header">
      <div className="header-content">
        <div className="logo-section">
          <div className="logo-icon">
            <a href="/"><img src="/logo.png" alt="LIF MDR Logo" width="32" height="32" /></a>
          </div>
          <a href="/"><h1>LIF MDR</h1></a>
        </div>
        <nav className="main-nav">
          <NavLink
            to="/explore"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Explore
          </NavLink>
          {/* <NavLink
            to="/learn"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Learn
          </NavLink>
          <NavLink
            to="/analyze"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Analyze
          </NavLink> */}
        </nav>

        {/* User Menu */}
        <Flex align="center" gap="3">
          <DropdownMenu.Root>
            <DropdownMenu.Trigger>
              <Button variant="ghost" size="2">
                <PersonIcon />
                <Text size="2">{user?.username || 'User'}</Text>
              </Button>
            </DropdownMenu.Trigger>
            <DropdownMenu.Content>
              <DropdownMenu.Label>
                <Text size="2" weight="medium">{user?.firstname} {user?.lastname}</Text>
                &nbsp;
                <Text size="1" color="gray" className="block">({user?.identifier})</Text>
              </DropdownMenu.Label>
              <DropdownMenu.Separator />
              <DropdownMenu.Item onClick={handleLogout}>
                <ExitIcon />
                Sign out
              </DropdownMenu.Item>
            </DropdownMenu.Content>
          </DropdownMenu.Root>
        </Flex>

        {/* <div className="breadcrumbs">
          {breadcrumbs.map((crumb, index) => (
            <React.Fragment key={crumb.path}>
              {index > 0 && " > "}
              <NavLink to={crumb.path}>{crumb.handle?.name}</NavLink>
            </React.Fragment>
          ))}
        </div> */}
      </div>
    </header>
  );
};

export default Header;
