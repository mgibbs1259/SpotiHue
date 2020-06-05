import React, { Component } from "react";
import "./Connect.css";

class Connect extends Component {
  constructor(props) {
    super(props);
    this.state = { connection: null };
  }

  handleConnect(props) {
    let connection = this.state.connection;
    fetch("/connect", { method: "POST" })
      .then((response) => response.json())
      .then((data) => this.setState({ connection: data.connection }));
    if (connection === "successful") {
      console.log(connection);
      this.props.history.push("/control");
    } else {
      return <h5 className="text__container-connection">{connection}</h5>;
    }
  }

  render() {
    return (
      <React.Fragment>
        <div className="header">
          <h1>SpotiHue</h1>
        </div>
        <div className="text__container-main">
          <h4>
            <p>Press the button on your Hue Bridge.</p>
            <p>Then, click Connect.</p>
          </h4>
        </div>
        <div className="button__container-upper">
          <button className="button" onClick={this.handleConnect.bind(this)}>
            Connect
          </button>
        </div>
        <div className="footer">
          <div>&copy; 2020 Mary Gibbs. All Rights Reserved.</div>
        </div>
      </React.Fragment>
    );
  }
}

export default Connect;
