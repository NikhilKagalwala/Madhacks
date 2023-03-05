// import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// import { faUser } from "@fortawesome/free-solid-svg-icons";

function PageThree(props) { 
    return (
        <div>
            {/* <div style={{ background: "#fff", float: "right", textAlign: "center", padding: "10px" }}>
                <FontAwesomeIcon icon={faUser} size="2x" /><br></br>
                Profile
            </div> */}
            <div className="container">      
                <div className="ToDoTitle">
                    <h3>To Do List</h3>
                </div>
                <div className="ToDo">
                        <ul id="Assignments"> 
                                {["Math 12/3", "CS 12/5", "Anthro 12/3", "CS 12/6"].map(item => (
                                    <li key={item}><a href="https://google.com">{item}</a></li>
                                ))}
                            </ul>
                    </div>
                <div className="RelDocsTitle">
                    <h3>Related Documents</h3>
                </div>
                <div className="RelDocsContent">
                        <ul id="RelDocsList"> 
                            {["Doc1", "Doc2", "Doc3", "Doc4"].map(item => (
                                <li key={item}><a href="https://google.com">{item}</a></li>
                            ))}
                        </ul>                </div>

                <div className="DriveTitle">
                    <h3>Important Folders</h3>
                </div>
                <div className="DriveContent">
                    <div className="DriveFormat">
                    <ul id="DriveList"> 
                            {["Folder1", "Folder2", "Folder3", "Folder4"].map(item => (
                                <li key={item}><a href="https://google.com">{item}</a></li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PageThree
