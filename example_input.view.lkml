# run looker-janitor: python main.py example_input.view.lkml example_output.view.lkml
view: orders {
  sql_table_name: `my_project.dataset.orders` ;;

  filter: customer_id_filter {
    type: number
    description: "Filter orders by customer ID"
    sql: ${TABLE}.customer_id ;;
  }

  filter: order_date_filter {
    type: date
    description: "Filter orders by date"
    sql: ${TABLE}.order_date ;;
  }

  filter: order_status_filter {
    type: string
    description: "Filter orders by status"
    sql: ${TABLE}.order_status ;;
  }

  dimension: order_id {
    type: number
    sql: ${TABLE}.order_id ;;
    primary_key: yes
  }

  dimension: customer_id {
    type: number
    sql: ${TABLE}.customer_id ;;
  }

  dimension: order_date {
    type: date
    sql: ${TABLE}.order_date ;;
  }

  dimension: order_status {
    type: string
    description: "The status of the order (e.g., 'shipped', 'pending')"
    sql: ${TABLE}.order_status ;;
  }

  dimension: total_amount {
    type: number
    sql: ${TABLE}.total_amount ;;
    value_format: "$#,##0.00"
  }

  measure: average_order_value {
    type: average
    description: "Average order value"
    sql: ${TABLE}.total_amount ;;
    value_format: "$#,##0.00"
  }

  measure: count {
    type: count
    description: "Count of orders"
    sql: ${TABLE}.order_id ;;
  }

  measure: total_sales {
    type: sum
    description: "Total sales amount"
    sql: ${TABLE}.total_amount ;;
    value_format: "$#,##0.00"
  }
}
