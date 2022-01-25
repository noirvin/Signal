import React from 'react';
import Company from './Company';
export default function CompaniesList({companies}) {
  return (
      companies.map(company =>{
          return <Company key={company.id} company={company} />
      } )
  )
}
