import React from "react";
import logo from "./logo-transparent-svg.svg";

function Header() {
  return (
    <div className="header-with-logo">
      <img src={logo} width={200} height={70} />
      <div className="app-header"></div>
    </div>
  );
}

export default Header;