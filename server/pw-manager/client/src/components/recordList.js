import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
 
const Record = (props) => (
 <tr>
   <td>{props.record.service}</td>
   <td>{props.record.username}</td>
   <td>{props.record.password}</td>
   <td>
     <Link className="btn btn-link" to={`/edit/${props.record._id}`}>Edit</Link> |
     <button className="btn btn-link"
       onClick={() => {
         props.deleteRecord(props.record._id);
       }}
     >
       Delete
     </button>
   </td>
 </tr>
);
 
export default function RecordList() {
  const [records, setRecords] = useState([]);
  const [sort,setSort] = useState('default');
  const sortTypes = {
    up: {
      fn: (a,b) => a.service > b.service ? 1 : -1
    },
    down: {
      fn: (a,b) => a.service < b.service ? 1 : -1
    },
    default: {
      fn: (a,b) => a
    }
  }
  
  // This method fetches the records from the database.
  useEffect(() => {
    async function getRecords() {
      const response = await fetch(`http://localhost:5000/record/`);
  
      if (!response.ok) {
        const message = `An error occurred: ${response.statusText}`;
        window.alert(message);
        return;
      }
  
      const records = await response.json();
      setRecords(records);
    }
  
    getRecords();
  
    return;
  }, [records.length]);
  
  // This method will delete a record
  async function deleteRecord(id) {
    await fetch(`http://localhost:5000/${id}`, {
      method: "DELETE"
    });
  
    const newRecords = records.filter((el) => el._id !== id);
    setRecords(newRecords);
  }
  
  // This method will map out the records on the table
  function recordList() {
    return records.sort(sortTypes[sort].fn).map((record) => {
      //console.log(record);
      return (
        <Record
          record={record}
          deleteRecord={() => deleteRecord(record._id)}
          key={record._id}
        />
      );
    });
  }

  //sort list
  function sortList() {
      //records.forEach(item => console.log(item.service));
      const sortedRecords = records.sort((a,b) => a.service > b.service ? 1 : -1);
      //sortedRecords.forEach(item => console.log(item));
      //console.log(sortedRecords);

      setRecords(sortedRecords);
      if (sort === 'default'){
        setSort('up');
      }
      else if (sort === 'up'){
        setSort('down');
      }
      else if (sort === 'down'){
        setSort('default');
      }


      console.log(sort);

      //console.log(records);
  }
  
  // This following section will dissplay the table with the records of individuals.
  return (
    <div>
      <h3>Record List</h3>
      <table className="table table-striped" style={{ marginTop: 20 }}>
        <thead>
          <tr>
              <th>
                <button className="btn btn-link" onClick={() => sortList()}>Service</button>
              </th>
            <th>Username</th>
            <th>Password</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>{recordList()}</tbody>
      </table>
    </div>
  );
}