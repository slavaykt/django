import React, {useState,useEffect} from 'react';
import TodosList from "./components/TodosList";
import TodoEdit from "./components/TodoEdit1";
import axios from "axios";

const App1 = () => {

    const [todoList,setTodoList] = useState([])
    const [currentId,setCurrentId] = useState(0)
    const [showEdit,setShowEdit] = useState(false)

    const refreshTodoList = () => {
        axios
          .get("/api/todos/")
          .then((res) => setTodoList(res.data))
          .catch((err) => console.log(err));
      };

    useEffect(() => {
        refreshTodoList()
    },[])

    const handleEdit = (id) => {
        setCurrentId(id)
        setShowEdit(true)
    }

    const handleCreate = () => {
        setCurrentId(0)
        setShowEdit(true)
    }

    return (
        <>
            <div className='row'>
                <aside className="col-2">
                </aside>
                <main className="col-10">
                    <div className="row">
                        <div className="col">
                            <TodosList
                                todoList={todoList}
                                handleEdit={handleEdit}
                                handleCreate={handleCreate}
                            />
                        </div>
                        <div className="col p-3">
                            {showEdit ? (
                                <TodoEdit
                                    itemId={currentId}
                                    refreshTodoList={refreshTodoList}
                                />
                            ) : null}
                        </div>
                    </div>
                </main>
            </div>          
        </>    
    )  
}

export default App1;