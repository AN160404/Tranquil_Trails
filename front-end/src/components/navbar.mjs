import React from 'react';
import PropTypes from 'prop-types';
const myStyle1={
  color:'white',
  backgroundColor:'rgb(250, 83, 111)',
  height:'50px',
  position: 'sticky',
  top:'0px',
  padding:'5px',  
}
const myStyle={
  color:'white',
  backgroundColor:'rgb(250, 83, 111)',
  height:'50px',
  position: 'sticky',
  top:'0px',
  padding:'0px',  
}

export default function Nav(props) {
  return (
    <><nav style={myStyle} className="navbar navbar-expand-lg bg-body-tertiary">
    <div className="container-fluid" style={myStyle1}>
      <a className="navbar-brand" href="/">Tranquil Trails</a>
      <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarNav">
        <ul className="navbar-nav">
          <li className="nav-item">
            <a className="nav-link active" aria-current="page" href="/">Home</a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="/">Features</a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="/">Pricing</a>
          </li>
          <li className="nav-item">
            <a className="nav-link disabled" aria-disabled="true">Disabled</a>
          </li>
        </ul>
      </div>
    </div>
  </nav></>
  )
}
