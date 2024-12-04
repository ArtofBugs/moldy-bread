// import express from 'express'
const express = require('express')
const bodyParser = require('body-parser')

const app = express()
const port = 8001

const datamuseRoot = 'https://api.datamuse.com/words'
const datamuseAdj = 'rel_jjb'

// Use bodyParser middleware to allow us to read request bodies as JSON
app.use(bodyParser.json())

app.post('/', async (req, res) => {
  console.log('body')
  console.log(req.body)
  if (!req.body) {
    res.status(200).send({})
    return
  }
  let datamuseURL = new URL(datamuseRoot)
  let substitutions = []
  for (const word of req.body) {
    datamuseURL.searchParams.append(datamuseAdj, word)
    const datamuseFetch = await fetch(datamuseURL.href)
    let result = await datamuseFetch.json()
    if (datamuseFetch.status != 200) {
      res.status(datamuseFetch.status).send(substitutions)
      return
    }
    if (result.length == 0) {
      substitutions.push(word)
    } else {
      substitutions.push(result[0].word)
    }
  }
  console.log('substitutions')
  console.log(substitutions)
  res.status(200).send(substitutions)
})

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}.`)
})
