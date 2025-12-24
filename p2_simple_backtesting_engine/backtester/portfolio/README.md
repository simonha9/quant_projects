A portfolio position manager consists of 3 layers (bottom up)

1. Ledger: this is a passive and completely factual representation of the positions we currently have. This also reflects the state after trades are filled. This holds
   - positions
   - cash
   - cost basis
   - realized/unrealized pnl
   - portfolio value
2. Constraints (normative): rules about our portfolio (invariants) that we must uphold
   - max position size
   - leverage limits
   - cash availability
   - exposure caps
   - long/short balance
3. Delta engine (interpretive): Given where we are right now, where do we want to be and how do we get there?
   - position deltas
   - rebalancing math
   - netting trades

Then, the portfolio position manager needs to translate trading signals into actual orders with intent. The flow is below:

1. get signals from the strategy generator
2. interpret these signals and transform them into an OrderIntent
3. verify that the OrderIntent stays within the constraints to then become an Order
4. take the Order and fill it to be executed (Execution Model)
5. take down the order in the ledger.

For each layer it only does the following:

1. SignalInterpreter _only_ transforms signals into OrderIntent that will be validated later
2. ConstraintValidator _only_ validates the OrderIntent
3. Executor _only_ executes the order
4. Ledger _only_ records what happens.

This way everything stays dumb and has a single responsibility. It also does _not_ mutate the state of anything.
