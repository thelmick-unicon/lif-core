import { Box, Flex } from "@radix-ui/themes";
import React from "react";

interface ExplorePageLayoutProps {
  sidebar?: React.ReactNode;
  mainContent: React.ReactNode;
}

const ExplorePageLayout: React.FC<ExplorePageLayoutProps> = ({
  sidebar,
  mainContent,
}) => {
  return (
    <Flex gap="3" flexGrow="1" p="4" style={{ maxHeight: "100%" }}>
      {sidebar && (
        <Box maxWidth="400px" style={{ maxHeight: "100%", overflow: "scroll" }}>
          {sidebar}
        </Box>
      )}
      <Flex flexGrow="1">{mainContent}</Flex>
    </Flex>
  );
};

export default ExplorePageLayout;
