# TEXTPROCESSOR
Text processing server (backend service for quicksearch)


## APIs
### Language Detection
uses cld3 to detect language of text
```
POST /api/langdet

Body: [
    "hello",
    "world
]

# Return
[
    "en",
    "en"
]
```
#### Todo
- [ ] Add percentage of language detection

### Text tokenisation
#### Todo

### Text entity recognition
#### Todo


### Full
#### Todo