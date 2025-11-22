import React from "react";
// import "./Layout.css";
import { Outlet, useLocation } from "react-router-dom";
import Header from "../Header/Header";
import Footer from "../Footer/Footer";
import { RouterWrapper } from "../RouterWrapper";
import { Flex } from "@radix-ui/themes";

const Layout: React.FC<any> = ({ children }) => {
  const location = useLocation();

  return (
    <RouterWrapper>
      <Flex direction={"column"} className="app-container">
        <Header />
        <main className="app-main">
          {location.pathname === "/" ? children : <Outlet />}
        </main>
        <Footer />
      </Flex>
    </RouterWrapper>
  );
};

export default Layout;
