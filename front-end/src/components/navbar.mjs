import React from 'react';
import PropTypes from 'prop-types';

const myStyle={
  marginLeft:'30px',
  marginRight:'100px',
  fontSize:'30px'
}
const myStyle2={
  marginLeft:'50px',
  marginRight:'50px'
}

export default function Nav(props) {
  return (
    <><nav  className="navbar navbar-expand-lg bg-body-tertiary">
    <div className="container-fluid" >

    <img classname="logo" src="Logo.png" alt="img not found" />

      
      <a className="navbar-brand" style={myStyle} href="/">Tranquil Trails</a>

      <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navbarNav">
        <ul className="navbar-nav">
          <li className="nav-item" style={myStyle2}>
            <a className="nav-link active" aria-current="page" href="/">About</a>
          </li>
          <li className="nav-item" style={myStyle2}>
            <a className="nav-link" href="/">Search Image</a>
          </li>
          <li className="nav-item" style={myStyle2}>
            <a className="nav-link" href="/">Get Reviews</a>
          </li>
        </ul>
      </div>
    </div>
  </nav></>
  )
}
