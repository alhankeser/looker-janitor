# run looker-janitor: python main.py example_input.view.lkml example_output.view.lkml
view: orders {
  sql_table_name: `my_project.dataset.orders` ;;

  dimension: order_id {
    primary_key: yes
    type: number
    sql: ${TABLE}.order_id ;;
  }

  dimension: order_date {
    sql: ${TABLE}.order_date ;;
    type: date
  }

  dimension: customer_id {
    sql: ${TABLE}.customer_id ;;
    type: number
  }

  dimension: order_status {
    type: string
    sql: ${TABLE}.order_status ;;
    description: "The status of the order (e.g., 'shipped', 'pending')"
  }

  dimension: total_amount {
    type: number
    value_format: "$#,##0.00"
    sql: ${TABLE}.total_amount ;;
  }

  measure: count {
    type: count
    sql: ${TABLE}.order_id ;;
    description: "Count of orders"
  }

  measure: total_sales {
    type: sum
    sql: ${TABLE}.total_amount ;;
    value_format: "$#,##0.00"
    description: "Total sales amount"
  }

  measure: average_order_value {
    type: average
    sql: ${TABLE}.total_amount ;;
    value_format: "$#,##0.00"
    description: "Average order value"
  }

  filter: order_date_filter {
    type: date
    sql: ${TABLE}.order_date ;;
    description: "Filter orders by date"
  }

  filter: order_status_filter {
    description: "Filter orders by status"
    type: string
    sql: ${TABLE}.order_status ;;
  }

  filter: customer_id_filter {
    sql: ${TABLE}.customer_id ;;
    description: "Filter orders by customer ID"
    type: number
  }
}
