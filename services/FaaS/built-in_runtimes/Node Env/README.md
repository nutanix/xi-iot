# Node.js Function Runtime

Node.js functions can be run in context of a data pipeline.
A transformation function must accept context as well as message payload as parameters.
Context can be used to query function parameters passed in when function has been instantiated.
Moreover context is used to send messages to next stage in data pipeline.

Following is a basic Node.js function template:

```
function main(ctx, msg) {
    return new Promise(function(resolve, reject) {
        // log list of transformation parameters
        console.log("Config", ctx.config)
        // log length of message payload
        console.log(msg.length)
        // forward message to next stage in pipeline
        ctx.send(msg)
        // complete promise
        resolve()
    })
}

exports.main = main
```

All functions must export main which returns a promise.

Folling is some sample console output of function:

> Config { IntParam: '42', StringParam: 'hello' }

> 2764855

### Packages available in Node Env
* alpine-baselayout
* alpine-keys
* apk-tools
* busybox
* libc-utils
* libgcc
* libressl2.5-libcrypto
* libressl2.5-libssl
* libressl2.5-libtls
* libstdc++
* musl
* musl-utils
* scanelf
* ssl_client
* zlib
