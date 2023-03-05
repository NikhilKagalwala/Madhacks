import "bootstrap/dist/css/bootstrap.min.css"
import "./App.css"
// import { BrowserRouter, Routes, Route } from "react-router-dom"
import PageOne from "./PageOne"
import PageTwo from "./PageTwo"
import React, { useState } from "react";



function App() {
  const [page, setPage] = useState(1)
  console.log(page)
  return (
    <div className="App">
      {page === 1 && <PageOne func={setPage} />}
      {page === 2 && <PageTwo />}
    </div>
  )
}

export default App