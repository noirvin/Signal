import React, { useState } from 'react';

export default function Company({company}) {

  const [signal,setSignal]= useState(null)  
  return <div className='company_info'>
      
        
        <label> 
        {company.symbol}
        {company.signal}
        </label>
        
      
  </div>;
}
