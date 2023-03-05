
function PageThree(props) { 
    const assignmentNames = [
        { name: "ENGL150 Paper 2 4/6/23 11:59pm", link: "https://docs.google.com/document/d/1HiGSOsEM8ymI6875qS7g8zBZXUfp3w90TiGZ1xQAV6c/edit?usp=sharing" },
    ]

    const courseInfo = [
        { name: "STAT240 Notes", link: "https://docs.google.com/document/d/1pTH2hhUckw7U7ajqReGeWM9VNzzAnwTPe39btJGPyEM/edit?usp=sharing" },
        { name: "ENGL150 Notes", link: "https://docs.google.com/document/d/1jSRh--dhrwY3gjkMggl0WPgNTjQgpxdhIXPFFpFP2o4/edit?usp=sharing" },
        { name: "COMPSCI577 Notes", link: "https://docs.google.com/document/d/1rWR6CDqWznTYnQBQF-4kzU4z7mRFLXUqwyCT8l7ubfg/edit?usp=sharing" },
    ]

    const driveInfo = [
        { name: "STAT240", link: "https://drive.google.com/drive/folders/10yIwB7W3za3HNl9rHfN2vJeHvKOeYKgJ" },
        { name: "ENGL150", link: "https://drive.google.com/drive/folders/1pF6xKx92drMCbdhCcny5ZMAQBeasV5P3" },
        { name: "COMPSCI577", link: "https://drive.google.com/drive/folders/1c4GQkBqSQSXRrYmSWa8pRBXrJ-YSShgf" },
    ]

    return (
        <div>
            <div className="container">      
                <div className="ToDoTitle">
                    <h3>To Do List</h3>
                </div>
                <div className="ToDoContent">
                        <ul id="AssignmentsInfo"> 
                        {assignmentNames.map(link => ( <li key={link.name}><a href={link.link}>{link.name}</a></li>))}
                        </ul>
                    </div>
                <div className="RelDocsTitle">
                    <h3>Related Documents</h3>
                </div> 
                <div className="RelDocsContent">
                    <ul id="RelDocsInfo"> 
                            {courseInfo.map(link => ( <li key={link.name}><a href={link.link}>{link.name}</a></li>))}
                        </ul>           
                    </div>
                <div className="DriveTitle">
                    <h3>Important Folders</h3>
                </div>
                <div className="DriveContent">
                    <div className="DriveFormat">
                        <ul id="DriveList"> 
                                {driveInfo.map(link => ( <li key={link.name}><a href={link.link}>{link.name}</a></li>))}
                        </ul>           
                    </div>
                </div>
            </div>
        </div>
    )
}

export default PageThree
