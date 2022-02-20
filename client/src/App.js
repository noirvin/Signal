import React, { useState, useRef, useEffect } from 'react';
import CompaniesList from './CompaniesList';
import Company from './Company';
import { v4 as uuidv4 } from 'uuid';
import io from 'socket.io-client';
import axios from 'axios'

const socket = io.connect('http://localhost:5000')

function App() {
  const [companies,setCompanies] = useState([])
  const companySymbolRef = useRef()

  socket.on('companiesAddedResponse', (res) => {
    console.log(res)
    companies.push({id: uuidv4(), symbol: res.data.data[1], signal: res.data.data[0]})

   		
    
    console.log(companies)
    setCompanies([...companies])
  })

  function handleAddCompanies(e){
    const symbols = companySymbolRef.current.value.split(' ')
    if (symbols === '')return
    socket.emit('CompaniesAdded', {'data' : symbols})
    companySymbolRef.current.value = null
  }

  return (
    <>
    <CompaniesList companies={companies}/>
    <input ref={companySymbolRef}type="text" />
    <button onClick={handleAddCompanies}>Add Company</button>
    <button>Clear all Companies</button>
    </>
    
  )
}

export default App;
