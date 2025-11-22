/* eslint-disable @typescript-eslint/no-explicit-any */
import { NavLink, useNavigate } from "react-router-dom";
import "./SubNav.css";
import { useMdrContext } from "../../context/MdrContext";
import { Box, Flex, IconButton, TextField } from "@radix-ui/themes";
import { DotsHorizontalIcon, MagnifyingGlassIcon } from "@radix-ui/react-icons";

const SubNav = () => {
  const { parentRoute } = useMdrContext();
  const navigate = useNavigate();

  // If no parent route (top-level route) or no children, don't render anything
  if (!parentRoute?.children?.length) {
    return null;
  }

  const PlaceholderIcon = () => (
    <svg
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="nav-icon"
    >
      <path
        d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"
        fill="currentColor"
      />
    </svg>
  );

  const handleSearchInput = (e: any) => {
    const { value } = e.target;
    if (!value?.trim()) return;
    // pressing enter should caputre the value and navigate to the search page
    // with keyword as query param
    if (e.key === "Enter") {
      navigate(`search?keyword=${value}`);
    }
  };

  return (
    <Flex direction="column" className="sub-nav-container" gap="2">
      <Box>
        <TextField.Root
          onKeyDown={handleSearchInput}
          placeholder="Search Models, Entities, Attributes, Value Sets, Mappings..."
          size="2"
        >
          <TextField.Slot>
            <MagnifyingGlassIcon height="16" width="16" />
          </TextField.Slot>
          <TextField.Slot>
            <IconButton size="1" variant="ghost">
              <DotsHorizontalIcon height="14" width="14" />
            </IconButton>
          </TextField.Slot>
        </TextField.Root>
      </Box>
      <nav className="sub-nav">
        <ul>
          {parentRoute.children.map((route: any) => {
            if (!route.handle) return null;

            return (
              <li key={route.path}>
                <NavLink
                  to={`/${parentRoute.path}/${route.path}`}
                  className={({ isActive }) =>
                    `nav-card ${isActive ? "active" : ""}`
                  }
                >
                  {/* <div className="icon-container">
                    <PlaceholderIcon />
                  </div> */}
                  <div className="nav-content">
                    <h3>{route.handle.name}</h3>
                  </div>
                </NavLink>
              </li>
            );
          })}
        </ul>
      </nav>
    </Flex>
  );
};

export default SubNav;
