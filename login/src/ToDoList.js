import React from 'react';

class ToDoList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            assignments: []
        };
    }
      
    componentDidMount() {
        const data = JSON.parse(test);
        this.setState({ assignments: data.assignments });
      }

      
    render() {
        const {assignments} = this.state;
        return (
            <div className="container">
                    <div className="ToDo">
                        <div>
                            {assignments.map((assignments, index) => (
                                 <div key={index}>
                                 <p>Name: {user.name}</p>
                                 <p>Age: {user.age}</p>
                               </div>
                            ))}
                    </div>
                </div>
        </div>

        );
    }
}