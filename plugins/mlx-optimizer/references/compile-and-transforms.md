# Compile And Transforms

Use this reference for `mx.compile`, `mx.grad`, `mx.value_and_grad`, `mx.vmap`,
and `mx.checkpoint`.

## Compile Fit

Good candidates:

- Pure numerical functions with stable argument structure.
- Repeated hot functions where compile overhead is amortized.
- Training steps that avoid host-side side effects.

Risky candidates:

- Functions that print, mutate global state, perform file I/O, or branch heavily
  on Python values.
- Functions whose shapes change constantly.
- Functions where one-off compile cost exceeds saved runtime.

## Training Transform Pattern

```python
def loss_fn(model, batch):
    logits = model(batch["x"])
    return cross_entropy(logits, batch["y"])

loss_and_grad = mx.value_and_grad(model, loss_fn)
loss, grads = loss_and_grad(model, batch)
optimizer.update(model, grads)
mx.eval(model.parameters(), optimizer.state, loss)
```

## Checkpointing

Use rematerialization when activation memory is the bottleneck and recomputation
is cheaper than storing intermediates. Verify with peak-memory and wall-time
measurements because checkpointing trades memory for compute.
