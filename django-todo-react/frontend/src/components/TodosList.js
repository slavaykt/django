import React, { useEffect, useLayoutEffect, useState } from 'react';
import {ListGroup, ListGroupItem, Button} from "reactstrap";

const TodosList = ({todoList,handleEdit,handleCreate}) => {

    return(
        <>
            <ListGroup>
                {todoList.map((item) => (
                    <ListGroupItem key={item.id}>
                        <a href="#" onClick={() => handleEdit(item.id)}>
                            {item.title}
                        </a>
                    </ListGroupItem>
                )
                )}
            </ListGroup>
            <Button
                color="primary"
                onClick={() => handleCreate()}
            >
                Добавить
            </Button>
        </>       
    )
}

export default TodosList