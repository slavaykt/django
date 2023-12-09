import React, { useEffect, useLayoutEffect, useState } from 'react';
import axios from "axios";
import {
    Form,
    FormGroup,
    Input,
    Label,
    Button,
    Table,
    Tooltip
  } from "reactstrap";

const copyObjectWithNullValues = (obj) => {
  const result = Array.isArray(obj) ? [] : {};

  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      if (obj[key] && typeof obj[key] === 'object') {
        result[key] = copyObjectWithNullValues(obj[key]); // Рекурсивный вызов для вложенных объектов или массивов
      } else {
        result[key] = null; // Установка null для примитивных значений
      }
    }
  }

  return result;
}

const TodoEdit = ({itemId,refreshTodoList}) => {

    const emptyStepsRow =  {name:"", days: 0, status: {id: 0,title:"---"}, status_id: 0}
    const emptyItem = {
        title: "",
        description: "",
        completed: false,
        steps: []
      }

    const [activeItem,setActiveItem] = useState(emptyItem)

    const [errors,setErrors] = useState(emptyItem)

    const [tooltipOpen, setTooltipOpen] = useState(false);

    const [tooltipContent, setTooltipContent] = useState("lorem ipsum");

    useEffect(() => {
        refreshItem()
    }, [itemId])

  const refreshItem = () => {
    if (itemId) {
      axios
        .get(`/api/todos/${itemId}/`)
        .then((res) => {
          setActiveItem(res.data)
          const errors_data = copyObjectWithNullValues(res.data)
          console.log(errors_data)
          setErrors(errors_data)
        })
        .catch((err) => console.log(err))
    } else {
      setActiveItem(emptyItem)
    }
  };
  const toggleTooltip = () => {
      setTooltipOpen(false)
  }

  const handleChange = (e) => {
    console.log(activeItem)
    let { name, value } = e.target
    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }

    setActiveItem({ ...activeItem, [name]: value })
  };

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  const validate = () => {
    let errors_check = Object.assign([], errors)
    let has_errors = false
    if (activeItem.title.length< 5) {
      errors_check.title = "Длина наименования не может быть менее 5 символов!"
      has_errors = true
    }

    activeItem.steps.forEach((row,i)=> {
      if (row.days<0) {
        errors_check.steps[i].days = "количество дней не может быть отрицательным"
        has_errors = true
      }
    })

    setErrors(errors_check)
    return has_errors
  }

  const handleSubmit = () => {
    if (validate()) {
      return
    }
    if (activeItem.id) {
      axios
        .put(`/api/todos/${activeItem.id}/`, activeItem)
        .then((res) => {
          refreshItem()
          refreshTodoList()
        })
        .catch((error) => {
          // Handle PUT request error
          console.error("Error updating item:", error)
          setTooltipContent("Error updating item: "+ error)
          setTooltipOpen(true)
          sleep(2000).then(() => { setTooltipOpen(false) });
        });
       return;
    }
    
    axios
      .post("/api/todos/", activeItem)
      .then((res) => {
        refreshItem();
        refreshTodoList();
      })
      .catch((error) => {
        // Handle POST request error
        console.error("Error creating item:", error);
      });
  };

  const handleDelete = () => {
    axios
      .delete(`/api/todos/${activeItem.id}/`)
      .then((res) => setActiveItem(emptyItem))
      .then((res) => refreshItem())
      .then((res) => refreshTodoList())
  };

  const handleRowChange = (e, rowIndex) => {
    let { name, value } = e.target
    let newSteps = Object.assign([], activeItem.steps)
    newSteps[rowIndex][name] = value
    setActiveItem({ ...activeItem, steps: newSteps })
  }

  const handleRowSelectChange = (e, rowIndex) => {
    const name = e.target.name
    const selectedOption = activeItem.status_options[e.target.selectedIndex-1]
    const value = selectedOption
    let newSteps = Object.assign([], activeItem.steps)
    newSteps[rowIndex][name] = value
    newSteps[rowIndex][name+"_id"] = value.id 
    setActiveItem({ ...activeItem, steps: newSteps })
  }

  const handleAddRow = () => {
    let newSteps = Object.assign([], activeItem.steps)
    newSteps.push(emptyStepsRow)
    setActiveItem({ ...activeItem, steps: newSteps })
  }

  const handleDeleteRow = (rowIndex) => {
    let newSteps = Object.assign([], activeItem.steps)
    newSteps.splice(rowIndex,1)
    setActiveItem({ ...activeItem, steps: newSteps })    
  }

    return(
        <Form>
            <FormGroup>
              <Label for="todo-title">Title</Label>
              <Input
                type="text"
                id="todo-title"
                name="title"
                value={activeItem.title}
                onChange={handleChange}
                placeholder="Enter Todo Title"
              />   
              {errors.title ? (<span style={{color: "red", fontSize: "0.7em"}}>{errors.title}</span>) : null}     
            </FormGroup>
            <FormGroup>
              <Label for="todo-description">Description</Label>
              <Input
                type="text"
                id="todo-description"
                name="description"
                value={activeItem.description}
                onChange={handleChange}
                placeholder="Enter Todo description"
              />
            </FormGroup>
            <FormGroup check>
              <Label check>
                <Input
                  type="checkbox"
                  name="completed"
                  checked={activeItem.completed}
                  onChange={handleChange}
                />
                Completed
              </Label>
            </FormGroup>
            <Table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Days</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {activeItem.steps.map((row,i) => (
                  <tr key={i}>
                   <td> 
                      <Input
                        type="text"
                        name="name"
                        value={row.name}
                        onChange={(e) => handleRowChange(e, i)}
                      />
                    </td>
                    <td>
                      <Input
                        type="number"
                        name="days"
                        value={row.days}
                        onChange={(e) => handleRowChange(e, i)}
                      />
                      {errors.steps[i].days ? (<span style={{color: "red", fontSize: '0.7em'}}>{errors.steps[i].days}</span>) : null}
                    </td>
                    <td>
                      <Input
                        type="select"
                        name="status"
                        value={row.status.title}
                        onChange={(e) => handleRowSelectChange(e, i)}
                      >
                        <option> --- </option>
                        {activeItem.status_options.map((item)=>(
                          <option>{item.title}</option>
                        ))}
                        </Input>
                    </td>
                    <Button
                      color="danger"
                      onClick={() => handleDeleteRow(i)}
                    >
                      Delete row
                    </Button>
                  </tr>
                )
                )}

              </tbody>
              <Button
                color="secondary"
                onClick={() => handleAddRow()}
            >
                Add row
            </Button>
            </Table>
            <Button
                color="success"
                id="submit_button"
                onClick={() => handleSubmit()}
            >
                Submit
            </Button>
          <Tooltip
            isOpen={tooltipOpen}
            target={'submit_button'}
            toggle={toggleTooltip}
          >
            {tooltipContent}
          </Tooltip>
            <Button
                color="danger"
                onClick={() => handleDelete()}
            >
                Delete
            </Button>
          </Form> 
               
    )
}

export default TodoEdit