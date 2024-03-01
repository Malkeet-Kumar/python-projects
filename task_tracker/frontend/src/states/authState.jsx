import React, { useState } from "react";
export const AuthContext = React.createContext()
export function AuthState(props){
    const user = JSON.parse(localStorage.getItem("user")) || {isLoggedIn:false,role:""}
    const [userAuth, setUserAuth] = useState(user)
    const [data, setData] = useState([])
    const [newTask,setNewTask] = useState(0)
    return(
        <AuthContext.Provider value={{userAuth,setUserAuth,data,setData, newTask, setNewTask}}>
            {props.children}
        </AuthContext.Provider>
    )
}