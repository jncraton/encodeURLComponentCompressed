let encmap = [["%20and","."],["%20the","e"],["%28%20","t"],["%20he","o"],["%20in","a"],["%20to","h"],["%20of","n"],["%20be","i"],["%20b","r"],["%20f","s"],["%20o","l"],["%20p","d"],["%20m","f"],["%20t","c"],["%20c","b"],["%20w","u"],["%20s","w"],["%20a","m"],["%20","y"],["%21","p"],["%22","g"],["%29","v"],["%27","k"],["%3F",","],["%2C","!"],["al","'"],["he","G"],["te","H"],["ou","I"],["ar","J"],["ea","K"],["se","L"],["an","M"],["or","N"],["en","O"],["st","P"],["th","Q"],["on","R"],["in","S"],["re","T"],["er","U"],["k","V"],["v","W"],["g","X"],["p","Y"],["y","Z"],["m","j"],["w","q"],["u","x"],["b","z"],["c","?"],["f","/"],["d",":"],["l","@"],["s","-"],["r","_"],["i","~"],["n","$"],["h","&"],["a","("],["o",")"],["t","*"],["e","+"],[".",";"],]

function encode(text) {
  text = text.replace(/(^|[\.\!\?] +|\n)([A-Za-z])/g, (c) => {
    return c == c.toUpperCase()
              ? c.toLowerCase()
              : c.toUpperCase()
  })

  text = encodeURIComponent(text)

  out = ""

  i = 0
  while (i < text.length) {
    found = false
    for (e of encmap) {
      if (text.substring(i, i+10).startsWith(e[0])) {
        out += e[1]
        i += e[0].length
        found = true
        break
      }
    }
    
    if (!found) {
      out+=text[i]
      i+=1
    }
  }
  
  return out
}

function decode(input) {
  text = ""

  i = 0
  while (i < input.length) {
    found = false
    for (e of encmap) {
      if (input.substring(i, i+10).startsWith(e[1])) {
        text += e[0]
        i += e[1].length
        found = true
        break
      }
    }
    
    if (!found) {
      text+=input[i]
      i+=1
    }
  }
  
  text = decodeURIComponent(text)

  text = text.replace(/(^|[\.\!\?] +|\n)([A-Za-z])/g, (c) => {
    return c == c.toUpperCase()
              ? c.toLowerCase()
              : c.toUpperCase()
  })

  return text
}

let test = "Hello, world! Let's make sure sentence casing works properly."

console.log(test)
console.log(encodeURIComponent(test))
console.log(encodeURIComponent(test).replace(/%20/g,'+'))
console.log(encode(test))
console.log(decode(encode(test)))