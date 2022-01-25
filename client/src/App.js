import React, { useState, useRef, useEffect } from 'react';
import CompaniesList from './CompaniesList';
import { v4 as uuidv4 } from 'uuid';

const LOCAL_STORAGE_KEY = 'companyApp.companies'

function App() {
  const [companies,setCompanies] = useState([])
  const companySymbolRef = useRef()

  useEffect(()=>{
    const storedCompanies = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY))
    if (storedCompanies) setCompanies(storedCompanies)
  },[])

  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_KEY,JSON.stringify(companies))
  },[companies])

  function handleAddCompany(e){

    const symbol = companySymbolRef.current.value
    if (symbol === '')return
    setCompanies(prevCompanies =>{
      return [...prevCompanies,{id:uuidv4(), symbol: symbol, signal:'stagnant'}]
    })
    companySymbolRef.current.value = null
  }

  return (
    <>
    <CompaniesList companies={companies}/>
    <input ref={companySymbolRef}type="text" />
    <button onClick={handleAddCompany}>Add Company</button>
    <button>Clear all Companies</button>
    </>
    
  )
}

export default App;
