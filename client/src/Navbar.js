import React, { Component } from 'react';




class Navi extends Component {
    render() {
      return (
        <div className="nav-container">
            <Navi className="mr-auto">
              <Navi.Link href="#home">Home</Navi.Link>
              <Navi.Link href="#features">Features</Navi.Link>
              <Navi.Link href="#pricing">Pricing</Navi.Link>
            </Navi>
        </div>
      )
    }
  }
  
  export default Navi;
