import React, { createContext, useContext, useState } from "react";

interface RouteInfo {
  path: string;
  handle?: {
    name: string;
    [key: string]: any;
  };
  [key: string]: any;
}

interface MdrContextType {
  currentRoute: RouteInfo | null;
  parentRoute: RouteInfo | null;
  breadcrumbs: RouteInfo[];
  setRouteInfo: (info: Omit<MdrContextType, "setRouteInfo">) => void;
}

interface MdrProviderProps {
  children: React.ReactNode;
}

const MdrContext = createContext<MdrContextType | undefined>(undefined);

export const MdrProvider: React.FC<MdrProviderProps> = ({ children }) => {
  const [routeInfo, setRouteInfo] = useState<
    Omit<MdrContextType, "setRouteInfo">
  >({
    currentRoute: null,
    parentRoute: null,
    breadcrumbs: [],
  });

  const value = {
    ...routeInfo,
    setRouteInfo,
  };

  return <MdrContext.Provider value={value}>{children}</MdrContext.Provider>;
};

export const useMdrContext = () => {
  const context = useContext(MdrContext);
  if (context === undefined) {
    throw new Error("useMdrContext must be used within a MdrProvider");
  }
  return context;
};
