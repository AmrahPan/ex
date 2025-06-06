import React, { useEffect, useState } from 'react'
import { Box, Heading, Table, Thead, Tbody, Tr, Th, Td, Input } from '@chakra-ui/react'

function App() {
  const [data, setData] = useState(null)

  const fetchData = () => {
    fetch('/api/dashboard')
      .then(r => r.json())
      .then(setData)
  }

  useEffect(() => {
    fetchData()
  }, [])

  const updateOrders = (id, orders_day) => {
    fetch(`/api/kitchen/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, name: data.kitchens.find(k => k.id === id).name, orders_day })
    }).then(fetchData)
  }

  if (!data) return <p>Loading...</p>

  const ebitdaColor = data.ebitda_ceh >= 0 ? 'green.200' : 'red.200'

  return (
    <Box p={4}>
      <Box borderWidth='1px' borderRadius='md' p={4} mb={4} bg={ebitdaColor}>
        <Heading size='md'>P&L цеха</Heading>
        <p>Выручка: {data.revenue_ceh.toFixed(2)}</p>
        <p>COGS: {data.cogs_ceh.toFixed(2)}</p>
        <p>EBITDA: {data.ebitda_ceh.toFixed(2)}</p>
      </Box>
      <Heading size='md' mb={2}>Кухни</Heading>
      <Table variant='simple'>
        <Thead>
          <Tr>
            <Th>Название</Th>
            <Th>Orders/day</Th>
            <Th>Profit/month</Th>
            <Th>Profit/portion</Th>
          </Tr>
        </Thead>
        <Tbody>
          {data.kitchens.map(k => (
            <Tr key={k.id}>
              <Td>{k.name}</Td>
              <Td>
                <Input type='number' value={k.orders_day}
                  onChange={e => updateOrders(k.id, parseInt(e.target.value))} />
              </Td>
              <Td>{k.profit_month.toFixed(2)}</Td>
              <Td>{k.profit_portion.toFixed(2)}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  )
}

export default App
