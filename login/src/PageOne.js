import React, { useState } from "react";

function PageOne(props) {
  const [loginMode, setLoginMode] = useState("signin")
  function showPageTwo() {
    props.func(2)
  }

  const changeLoginMode = () => {
    setLoginMode(loginMode === "signin" ? "signup" : "signin")
  }
  if (loginMode === "signin") {
    return (
      <div className="Login-form-container">
        <form className="Login-form">
          <div className="Login-form-content">
            <h3 className="Login-form-title">Sign In</h3>
            <div className="text-center">
              Not registered yet?{" "}
              <span className="link-primary" onClick={changeLoginMode}>
                Sign Up
              </span>
            </div>
            <div className="form-group mt-3">
              <label>Email address</label>
              <input
                id="email"
                type="email"
                className="form-control mt-1"
                placeholder="Enter email"
              />
            </div>
            <div className="form-group mt-3">
              <label>User ID</label>
              <input
                id="User ID"
                className="form-control mt-1"
                placeholder="Enter user ID"
              />
            </div>
            <div className="form-group mt-3">
              <label>Password</label>
              <input
                type="password"
                className="form-control mt-1"
                placeholder="Enter password"
              />
            </div>
            <div className="d-grid gap-2 mt-3">
              <button onClick={showPageTwo} type="submit" className="btn btn-primary">
                Submit
              </button>
            </div>
        </div>
        </form>
      </div>
    )
  }

  return (
    <div className="Login-form-container">
      <form className="Login-form">
        <div className="Login-form-content">
          <h3 className="Login-form-title">Sign Up</h3>
          <div className="text-center">
            Already registered?{" "}
            <span className="link-primary" onClick={changeLoginMode}>
              Sign In
            </span>
          </div>
          <div className="form-group mt-3">
            <label>Full Name</label>
            <input
              type="email"
              className="form-control mt-1"
              placeholder="e.g Jane Doe"
            />
          </div>
          <div className="form-group mt-3">
            <label>Email address</label>
            <input
              type="email"
              className="form-control mt-1"
              placeholder="Email Address"
            />
          </div>
          <div className="form-group mt-3">
              <label>Phone number</label>
              <input
                type="phone number"
                className="form-control mt-1"
                placeholder="xxx-xxx-xxx"
              />
            </div>
            <div className="form-group mt-3">
              <label>User ID</label>
              <input
                id="User ID"
                className="form-control mt-1"
                placeholder="Enter User ID"
              />
            </div>
          <div className="form-group mt-3">
            <label>Password</label>
            <input
              type="password"
              className="form-control mt-1"
              placeholder="Password"
            />
          </div>
          <div className="d-grid gap-2 mt-3">
            <button onClick={showPageTwo} type="submit" className="btn btn-primary">
              Submit
            </button>
          </div>
         </div>
      </form>
    </div>
  )
}

export default PageOne