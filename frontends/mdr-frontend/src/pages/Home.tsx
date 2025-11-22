import React from "react";
// import MainContent from "../components/MainContent/MainContent";
import Layout from "../components/Layout/Layout";
import { useNavigate } from "react-router-dom";

const Home: React.FC = () => {
  const navigate = useNavigate();
  const navigateToLifModelPage = () => {
    navigate("/explore/lif-model");
  };

  React.useEffect(() => {
    // Until we get actual home page content, redirect to /explore directly
    if (window.location.pathname === "/") {
      // console.log("redirecting from /");
      navigate("/explore", { replace: true });
    }
  }, [navigate]);

  return <Layout>home</Layout>;
};

export default Home;
