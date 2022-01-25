import React from 'react';

export default function Company({company}) {
  return <div>
      
        
        <label> 
        {company.symbol}
        {company.signal}
        </label>
       
      
  </div>;
}
