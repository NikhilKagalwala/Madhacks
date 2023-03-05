function PageTwo(props) { 
  function showPageThree() {
    props.func(3)
  }

    return (
      <div className="Info-form-container">
        <form className="Info-form">
          <div className="Info-form-content">
            <h3 className="Info-form-title">Required Information</h3>
            <div className="form-group mt-3">
              <label>
                Institution's Canvas URL:&nbsp;
                <a href="https://community.canvaslms.com/t5/Canvas-Basics-Guide/Where-do-I-find-my-institution-s-URL-to-access-Canvas/ta-p/82">help</a> 
              </label>
              <input
                type="Canvas URL"
                className="form-control mt-1"
                placeholder="e.g canvas.wisc.edu"
              />
            </div>
            <div className="form-group mt-3">
              <label>
                Canvas API Token:&nbsp;
                <a href="https://kb.iu.edu/d/aaja">help</a> 
              </label>
              <input
                type="Canvas API Token"
                className="form-control mt-1"
                placeholder="Enter token"
              />
            </div>
            <div className="form-group mt-3">
              <label>
                Canvas User ID:&nbsp;
                <a href="https://community.canvaslms.com/t5/Canvas-Question-Forum/How-to-find-8-digit-Canvas-Id/m-p/465618#M156703">help</a>
              </label>
              <input
                type="Canvas User ID"
                className="form-control mt-1"
                placeholder="Enter ID"
              />
            </div>
            <div className="form-group mt-3">
              <label>
                Google API Key:&nbsp;
                <a href="https://developers.google.com/maps/documentation/embed/get-api-key">help</a>
              </label>
              <input
                type="Google API Key"
                className="form-control mt-1"
                placeholder="Enter key"
              />
            </div>
            <div className="d-grid gap-2 mt-3">
              <button onClick={showPageThree} type="submit" className="btn btn-primary">
                Submit
              </button>
            </div>
        </div>
        </form>
      </div>
    )
}

export default PageTwo