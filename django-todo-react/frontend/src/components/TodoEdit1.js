import React, { useEffect, Warning } from 'react';
import { useForm, useFieldArray } from "react-hook-form"
import { DevTool } from '@hookform/devtools'
import axios from "axios";
import {
  Form,
  FormGroup,
  Label,
  Button,
  Input,
  UncontrolledTooltip
} from "reactstrap";

const TodoEdit = ({ itemId, refreshTodoList }) => {

  const {
    register,
    control,
    handleSubmit,
    formState: { errors },
    setValue,
    trigger,
    getValues,
    clearErrors } = useForm(
      {
        mode: 'onBlur',
        reValidateMode: 'onBlur'
      }
    )

  const {fields, append, remove} = useFieldArray({
    name: 'steps',
    control
  })

  useEffect(() => {
    refresh()
  }, [itemId])

  const getEmptyRow = (tableName) =>{
    const emptyRows = {
      'steps': {name:"", days: 0, status: {id: 0,title:"---"}, status_id: 0}
    }
    return (
      emptyRows[tableName]
    )
  } 

  const refresh = async () => {
    if (itemId) {
      const response = await fetch(`/api/todos/${itemId}/`)
      const data = await response.json()
      Object.keys(data).forEach((key)=>{
        setValue(key,data[key])
      })
      // clearErrors()
    }
  }

  const handleGetValues = ()=> {
    console.log(getValues("status_options"))
  }

  const getStatusOptions = () => {
    return [{id: 0, title: "---"},...getValues("status_options")]
  }

  const onSubmit = (data) => {
    // Handle form submission
    console.log(data);
  if (data.id) {
      axios
        .put(`/api/todos/${data.id}/`, data)
        .then((res) => {
          refreshTodoList()
        })
        .catch((error) => {
          // Handle PUT request error
          console.error("Error updating item:", error)
        });
       return;
    }
    
    axios
      .post("/api/todos/", data)
      .then((res) => {
        refreshTodoList()
      })
      .catch((error) => {
        // Handle POST request error
        console.error("Error creating item:", error)
      });
  };

  const handleStatusChange = (event, index) => {
    const newStatusId = getStatusOptions()[event.target.selectedIndex].id
    setValue(`steps.${index}.status.id`, newStatusId)
    setValue(`steps.${index}.status_id`, newStatusId)
  }

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <div className="form-group">
          <label htmlFor='todo-title'>Title</label>
          <input type='text' id='todo-title'
            className={`form-control ${errors?.title ? 'is-invalid' : ''
              }`}
            {...register('title', {
              required: 'поле title должно быть заполнено!',
              validate: (v) => {
                return v !== 'fuck' || 'ругательные слова недопустимы!'
              }
            })} />
          {errors?.title && (
            <UncontrolledTooltip placement="bottom" target="todo-title">
              {errors.title?.message}
            </UncontrolledTooltip>
          )}
        </div>
        <div className="form-group">
          <label className="control-label" htmlFor='description'>Description</label>
          <input type='text' id='description'
                    className={`form-control ${
                      errors?.description ? 'is-invalid' : ''
                    }`}              
            {...register('description', {
              required: 'поле description должно быть заполнено!',
              minLength: {
                value: 5,
                message: 'поле description должно содержать не менее 5 символов!'
              }
            })} />
          {errors?.description && (
            <UncontrolledTooltip placement="bottom" target="description">
              {errors.description?.message}
            </UncontrolledTooltip>
          )}
        </div>

        <div className="form-check">
          <input className="form-check-input" type="checkbox" {...register('completed')} id="completed">
            </input>
            <label className="form-check-label" htmlFor="completed">
              Completed
            </label>
        </div>
        <div>
          <div className="row">
            <div className="col-6">Name</div>
            <div className="col-2">Days</div>
            <div className="col-2">Status</div>
            <div className="col-2">Delete</div>
          </div>
          {fields.map((field, index) => (
            <div className="row" key={field.id}>
              <div className="col-6 p-1">
                <input className="form-control" type="text" id={`name-${index}`} {...register(`steps.${index}.name`)} />
              </div>
              <div className="col-2 p-1">
                <input className="form-control" type="number" id={`days-${index}`} {...register(`steps.${index}.days`)} />
              </div>
              <div className="col-2 p-1">
                <select id={`status-${index}`} {...register(`steps.${index}.status.title`, {
                  validate: (v) => v !== '---' || 'статус не заполнен!',
                })}
                  onChange={(e) => handleStatusChange(e, index)}
                  className={`form-control ${errors?.steps?.[index]?.status?.title ? 'is-invalid' : ''
                    }`}
                >
                  {getStatusOptions().map((item) => (
                    <option key={item.id} value={item.title}>{item.title}</option>
                  ))}
                </select>
                {errors?.steps?.[index]?.status?.title && (
                  <UncontrolledTooltip placement="bottom" target={`status-${index}`}>
                    {errors.steps[index].status.title.message}
                  </UncontrolledTooltip>
                )}
              </div>
              <div className="col-2 p-1">
                <button className="btn btn-danger" onClick={() => remove(index)}>
                  Delete
                </button>
              </div>
            </div>
          ))}
        <div className="d-flex justify-content-center">
        <button className="d-flex justify-content-center w-50 btn btn-secondary" onClick={() => append(getEmptyRow('steps'))}>
            Add row
          </button>
        </div>
        </div>
          <div className="d-flex justify-content-center">
            <button className="mt-2 w-50 center-block btn btn-success"> Submit </button>
          </div>
      </form>
      <DevTool control={control} />
    </>
  )
}

export default TodoEdit