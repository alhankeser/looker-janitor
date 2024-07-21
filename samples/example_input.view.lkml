# This is a view file that needs clean-up.
# Try one of the examples here to clean it up:
  # https://github.com/alhankeser/looker-janitor/?tab=readme-ov-file#more-examples


view: orders {
  

        sql_table_name: `my_project.dataset.orders` ;;

  measure: total_sales {
     type: sum
    description: "Total sales amount"
          sql: ${TABLE}.total_amount ;;
    value_format: "$#,##0.00"
  }
  

  filter: order_status_filter {
    type: string
    label: "Status Filter"
    description: "Filter orders by status"
    sql: ${TABLE}.order_status ;;
  }


  dimension: customer_id {
    type: number
    sql: ${TABLE}.customer_id ;;
  }

  filter: order_date_filter {
    type: date
      description: "Filter orders by date"
    sql: ${TABLE}.order_date ;;
  }

  dimension: order_date {
    sql: ${TABLE}.order_date ;;
    type: date
  }

  dimension: order_status {
    description: "The status of the order (e.g., 'shipped', 'pending')"
    type: string
    sql: ${TABLE}.order_status ;;
  }

  dimension: total_amount {
    sql: ${TABLE}.total_amount ;;
    type: number
          label: "orders.total_amount.label"
    value_format: "$#,##0.00"
  }

  measure: average_order_value {
    type: average
    description: "Average order value"
    sql: ${TABLE}.total_amount ;;
    value_format: "$#,##0.00"
  }

  measure: count {
    description: "Count of orders"
    type: count
    sql: ${TABLE}.order_id ;;
  }

  filter: customer_id_filter {
    description: "Filter orders by customer ID"
          type: number
          sql: ${TABLE}.customer_id ;;
  }


  dimension: order_id {
    sql: ${TABLE}.order_id ;;
    type: number
    primary_key: yes
    label: "orders.order_id.label"
  }
 
}
