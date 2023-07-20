import React, {useState, useEffect, useRef, createContext} from "react"

const Context = createContext()
const Provider = ( {chilren} ) => {

    const [isLoggedIn, setIsLoggedIn] = useState(false)

    const globalContext = {
        isLoggedIn,
        setIsLoggedIn,
    }
    return <Context.Provider value ={globalContext}></Context.Provider>
}
export { Context, Provider }