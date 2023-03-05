import "bootstrap/dist/css/bootstrap.min.css"
import "./App.css"
import PageOne from "./PageOne"
import PageTwo from "./PageTwo"
import PageThree from "./PageThree"

import React, { useState } from "react";



function App() {
  const [page, setPage] = useState(1)
  return (
    <div className="App">
      {page === 1 && <PageOne func={setPage} />}
      {page === 2 && <PageTwo func={setPage} />}
      {page === 3 && <PageThree func={setPage} />}
    </div>
  )
}

export default App