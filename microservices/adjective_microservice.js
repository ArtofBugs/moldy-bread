// import express from 'express'
const express = require('express')
const bodyParser = require('body-parser')

const app = express()
const port = 8001

const datamuseRoot = 'https://www.datamuse.com/api/words'
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
  req.body.forEach(async (word) => {
    datamuseURL.searchParams.append(datamuseAdj, word)
    const datamuseFetch = await fetch(datamuseURL.href)
    let result = await datamuseFetch.json()
    if (result.status != 200) {
      res.status(result.status).send(substitutions)
      return
    }
    if (result.length == 0) {
      substitutions.append(word)
    } else {
      substitutions.append(result[0].word)
    }
  })
  console.log('substitutions')
  console.log(substitutions)
  res.status(200).send(substitutions)
})

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}.`)
})
