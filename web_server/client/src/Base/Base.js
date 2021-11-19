import React from "react";
import { Link } from "react-router";
import Auth from "../Auth/Auth";

class Base extends React.Component {
  render() {
    return (
      <div>
        <nav className="nav-bar indigo lighten-1">
          <div className="nav-wrapper">
            <a href="/" className="brand-logo">
              &nbsp;&nbsp;Tin tức Bất động sản
            </a>
            <ul className="right" id="nav-mobile">
              {Auth.isUserAuthenticated() ? (
                <div>
                  <li>{Auth.getEmail()}</li>
                  <li>
                    <Link to="/logout">Đăng xuất</Link>
                  </li>
                </div>
              ) : (
                <div>
                  <li>
                    <Link to="/login">Đăng nhập</Link>
                  </li>
                  <li>
                    <Link to="/signup">Đăng ký</Link>
                  </li>
                </div>
              )}
            </ul>
          </div>
        </nav>
        <br />
        {this.props.children}
      </div>
    );
  }
}

export default Base;
