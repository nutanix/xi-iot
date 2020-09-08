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

