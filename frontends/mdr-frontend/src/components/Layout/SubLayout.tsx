import React from "react";
// import "./Layout.css";
import { Outlet } from "react-router-dom";
import SubNav from "../../components/SubNav/SubNav";
// import Router from "../../pages/Routes";
import { Container, Section } from "@radix-ui/themes";

import { useMdrContext } from "../../context/MdrContext";

const SubLayout: React.FC = () => {
  const { breadcrumbs } = useMdrContext();
  const section = breadcrumbs?.[1]?.handle?.name;

  return (
    <div className="layout">
      <Container>
        {/* <Section>
          <h2>{section}</h2>
        </Section> */}
        <br />
        <SubNav />
      </Container>
      <div className="content">
        <Outlet />
      </div>
    </div>
  );
};

export default SubLayout;
